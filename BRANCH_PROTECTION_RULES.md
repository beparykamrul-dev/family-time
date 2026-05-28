# Branch Protection Rules - family-time Repository

## 🔒 Main Branch Protection Policy

This document outlines the branch protection strategy for the `main` branch to ensure code quality, security, and stability.

---

## 📋 Recommended Protection Rules for `main`

### 1. **Require Pull Request Reviews**
- ✅ **Require approvals**: 1 reviewer minimum
- ✅ **Dismiss stale PR approvals**: Enabled
- ✅ **Require review from code owners**: Enabled
- ✅ **Require approval of the most recent reviewable push**: Enabled

**Rationale**: Ensures at least one peer review before merging to production.

---

### 2. **Require Status Checks to Pass**
- ✅ **Require branches to be up to date**: Enabled
- ✅ **Require build to pass before merging**: Enabled
- ✅ **Status checks**:
  - `build` (CI/CD pipeline)
  - `test` (Unit & integration tests)
  - `lint` (Code quality checks)
  - `security` (SAST/dependency scanning)

**Rationale**: Prevents broken or insecure code from reaching production.

---

### 3. **Require Branches to be Up to Date**
- ✅ **Enabled**: All branches must be rebased/merged with `main` before merging

**Rationale**: Prevents conflicts and ensures tests pass against latest code.

---

### 4. **Restrict Force Pushes**
- ✅ **Allow force pushes**: Disabled
- ✅ **Allow deletions**: Disabled

**Rationale**: Prevents accidental loss of commits and maintains audit trail.

---

### 5. **Require Signed Commits**
- ✅ **Require branches to be up to date before merging**: Enabled
- ✅ **Require pull request reviews before merging**: Enabled

**Recommended**: ⚠️ Not enforced initially (can enable after team setup GPG keys)

---

### 6. **Require Conversation Resolution**
- ✅ **Enabled**: All conversations must be resolved before merging

**Rationale**: Ensures feedback is addressed before code lands.

---

## 🔑 Code Owners Configuration

Create `.github/CODEOWNERS` file:

```
# Infrastructure & Deployment
infrastructure/terraform/**        @beparykamrul-dev
infrastructure/ansible/**           @beparykamrul-dev
docker-compose*.yml                 @beparykamrul-dev
.github/workflows/**                @beparykamrul-dev

# Backend
backend/**                          @beparykamrul-dev
backend/requirements.txt            @beparykamrul-dev

# Frontend
frontend/**                         @beparykamrul-dev
package.json                        @beparykamrul-dev
package-lock.json                   @beparykamrul-dev

# Configuration & Documentation
*.md                                @beparykamrul-dev
.env.example                        @beparykamrul-dev
```

---

## 📊 Current Repository Status

| Setting | Value |
|---------|-------|
| Default Branch | `main` |
| Allow Merge Commits | ✅ Yes |
| Allow Squash Merges | ✅ Yes |
| Allow Rebase Merges | ✅ Yes |
| Auto-Merge | ❌ No |
| Delete Branches on Merge | ❌ No (⚠️ Recommended: Yes) |
| Require Status Checks | ⚠️ Not Configured |
| Require PR Reviews | ⚠️ Not Configured |
| Dismiss Stale Reviews | ⚠️ Not Configured |
| Require Code Owner Review | ⚠️ Not Configured |

---

## 🛠️ How to Configure Branch Protection

### Via GitHub UI (Recommended for Initial Setup)

1. Go to: **Settings → Branches → Add rule**
2. **Branch name pattern**: `main`
3. Configure protections (as per section above)
4. Click **Create**

### Via GitHub CLI

```bash
# Requires GitHub CLI v1.14.0+
gh repo edit beparykamrul-dev/family-time \
  --enable-squash-merge-commit \
  --enable-rebase-merge \
  --delete-branch-on-merge
```

### Via Terraform (Recommended for IaC)

```hcl
resource "github_branch_protection" "main" {
  repository_id = github_repository.family_time.node_id
  pattern       = "main"

  require_signed_commits       = false
  required_status_checks {
    strict   = true
    contexts = ["build", "test", "lint", "security"]
  }

  require_pull_request_reviews {
    required_approving_review_count = 1
    dismiss_stale_reviews           = true
    require_code_owner_reviews      = true
    require_last_push_approval      = true
  }

  restrict_pushes {
    push_allowances = []
  }

  force_push_bypassers = []
}
```

---

## 🚀 Deployment Strategy with Branch Protection

### Standard Workflow

```
1. Feature Branch (based on main)
   ├─ Push changes
   ├─ GitHub Actions runs (build, test, lint, security)
   └─ Create Pull Request

2. Code Review
   ├─ Assign reviewers (auto: CODEOWNERS)
   ├─ Request changes if needed
   └─ Approve changes (≥1 required)

3. Automated Checks
   ├─ ✅ All CI/CD tests pass
   ├─ ✅ Branch is up to date with main
   ├─ ✅ All conversations resolved
   └─ ✅ Code owner approval (if applicable)

4. Merge
   ├─ Use "Squash and merge" for clean history
   ├─ Delete feature branch
   └─ Trigger production deployment

5. Monitoring
   ├─ Watch deployment status
   ├─ Monitor error rates
   └─ Rollback if issues detected
```

---

## 📝 PR Template

Create `.github/pull_request_template.md`:

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation

## Related Issues
Fixes #(issue number)

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests passed
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tested on staging environment
```

---

## 🔐 Security Considerations

### Branch Naming Convention
- `main` - Production branch (protected)
- `develop` - Development branch
- `feature/*` - Feature branches
- `bugfix/*` - Bug fix branches
- `hotfix/*` - Hotfix branches (from main)

### Commit Standards
- Use descriptive commit messages
- Reference related issues: `Fixes #123`
- Use conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`

### Access Control
- Only repository owner/maintainers can merge
- Force push disabled on main
- Branch deletions disabled
- Require reviews from code owners

---

## ⚡ Emergency Procedures

### Hotfix Process
```
1. Create hotfix branch from main
   git checkout -b hotfix/issue-name main

2. Make minimal fix
3. Test thoroughly
4. Create PR with "HOTFIX" prefix
5. Fast-track review (requires urgent approval)
6. Merge with "Create a merge commit" to preserve history
7. Tag release immediately
```

### Rollback Procedure
```
1. Identify problematic commit
2. Revert with: git revert <commit-sha>
3. Create emergency PR
4. Merge and deploy immediately
5. Post-mortem after stabilization
```

---

## 📊 Monitoring & Metrics

Track the following metrics:
- Average PR review time
- PR rejection rate
- CI/CD pipeline success rate
- Time to production
- Mean time to recovery (MTTR)

---

## ✅ Implementation Checklist

- [ ] Create `.github/CODEOWNERS` file
- [ ] Create `.github/pull_request_template.md`
- [ ] Configure branch protection via GitHub UI
- [ ] Set up branch-specific secrets (if needed)
- [ ] Enable required status checks (after CI/CD setup)
- [ ] Test PR workflow with dummy PR
- [ ] Document in team wiki/docs
- [ ] Train team on new workflow
- [ ] Monitor initial PRs for compliance

---

## 🔗 References

- [GitHub Branch Protection Rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches)
- [CODEOWNERS File](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub Actions](https://docs.github.com/en/actions)

---

**Last Updated**: 2026-05-28  
**Status**: Ready for Implementation  
**Owner**: @beparykamrul-dev
